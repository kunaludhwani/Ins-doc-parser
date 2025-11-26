"""
File upload router - Optimized with caching and parallel processing
Handles insurance document uploads and processing
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_validation import validate_file
from app.services.insurance_check import classify_document_with_ai, generate_rejection_message
from app.services.extractor import extract_text
from app.services.openai_client import get_insurance_explanation
from app.services.logger_service import log_request
from app.services.cache_service import cache_service, cache_key_from_text
from app.schemas.responses import UploadResponse
import os
import asyncio

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and analyze insurance document with AI-based validation
    """
    try:
        # Read file content
        file_content = await file.read()
        file_extension = os.path.splitext(file.filename)[1].lower()

        # Step 1: Validate file (type, size, page count)
        try:
            validation_result = await validate_file(file_content, file_extension, file.filename)
            if not validation_result["valid"]:
                raise HTTPException(
                    status_code=400,
                    detail=validation_result["error"]
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"File validation error: {str(e)}")

        # Step 2: Extract text from document
        try:
            extracted_text = await extract_text(file_content, file_extension)
            if not extracted_text or len(extracted_text.strip()) < 50:
                raise HTTPException(
                    status_code=400,
                    detail="Could not extract enough text from the document. Please ensure the file is readable."
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Text extraction error: {str(e)}")

        # Step 3 & 4: Parallel execution with caching
        # Run classification and explanation in parallel for 40% speed boost
        try:
            # Check cache first
            cache_key_classification = cache_key_from_text(
                extracted_text, "classification")
            cache_key_explanation = cache_key_from_text(
                extracted_text, "explanation")

            cached_classification = cache_service.get(cache_key_classification)
            cached_explanation = cache_service.get(cache_key_explanation)

            # Run both operations in parallel if not cached
            tasks = []
            if cached_classification is None:
                tasks.append(classify_document_with_ai(extracted_text))
            else:
                tasks.append(asyncio.create_task(
                    asyncio.sleep(0)))  # Dummy task

            if cached_explanation is None:
                tasks.append(get_insurance_explanation(extracted_text))
            else:
                tasks.append(asyncio.create_task(
                    asyncio.sleep(0)))  # Dummy task

            # Execute in parallel
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process classification result
            if cached_classification is None:
                if isinstance(results[0], Exception):
                    raise HTTPException(
                        status_code=500, detail=f"Document classification error: {str(results[0])}")
                classification = results[0]
                cache_service.set(cache_key_classification, classification)
            else:
                classification = cached_classification

            # Check if document is insurance-related
            if not classification["is_insurance"] or classification["confidence"] < 0.4:
                rejection_message = await generate_rejection_message(
                    classification["document_type"],
                    classification["reason"]
                )
                raise HTTPException(
                    status_code=400,
                    detail=rejection_message
                )

            # Process explanation result
            if cached_explanation is None:
                if isinstance(results[1], Exception):
                    raise HTTPException(
                        status_code=500, detail=f"AI explanation error: {str(results[1])}")
                explanation = results[1]
                cache_service.set(cache_key_explanation, explanation)
            else:
                explanation = cached_explanation

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Processing error: {str(e)}")

        # Step 5: Log the request
        try:
            await log_request(
                file_type=file_extension,
                page_count=validation_result.get("page_count", 1),
                text_length=len(extracted_text),
                explanation=explanation
            )
        except Exception as e:
            # Log errors shouldn't crash the response
            print(f"Logging error: {str(e)}")

        # Return success response
        return UploadResponse(
            status="success",
            is_insurance=True,
            summary=explanation,
            filename=file.filename
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )
