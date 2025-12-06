import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional, Union

from rest_framework.request import Request
from rest_framework.response import Response

from apps.shared.exceptions.translator import get_message_detail

logger = logging.getLogger(__name__)


@dataclass
class ResponseBody:
    message_key: str
    request: Optional[Request] = None
    context: Optional[Dict[str, Any]] = None

    def get_language(self) -> str:
        """Extract Accept-Language header"""
        if self.request and hasattr(self.request, "headers"):
            accept_lang = self.request.headers.get("Accept-Language", "en")
            return accept_lang.split(";")[0].split(",")[0].strip()
        return "en"

    def to_dict(self, **kwargs) -> Dict[str, Any]:
        """Convert response using translated message"""
        lang = self.get_language()
        detail = get_message_detail(
            message_key=self.message_key,
            lang=lang,
            context=self.context
        )

        return {
            "id": detail["id"],
            "message": detail["message"],
            **kwargs
        }

    def get_status_code(self) -> int:
        """Get HTTP code from message templates"""
        lang = self.get_language()
        detail = get_message_detail(
            message_key=self.message_key,
            lang=lang,
            context=self.context
        )
        return detail["status_code"]


class CustomResponse:
    """Wrapper for all API responses"""

    @staticmethod
    def success(
        message_key: str = "SUCCESS_MESSAGE",
        request: Request = None,
        data: Any = None,
        context: Dict[str, Any] = None,
        status_code: int = None,
        **kwargs
    ) -> Response:

        body_maker = ResponseBody(
            message_key=message_key,
            request=request,
            context=context
        )

        body = body_maker.to_dict(data=data, **kwargs)

        final_status = status_code or body_maker.get_status_code()

        return Response(body, status=final_status)

    @staticmethod
    def error(
        message_key: str,
        request: Request = None,
        context: Dict[str, Any] = None,
        errors: Union[Dict[str, Any], str, Exception] = None,
        status_code: int = None,
        **kwargs
    ) -> Response:

        body_maker = ResponseBody(
            message_key=message_key,
            request=request,
            context=context
        )

        extra_fields = {}
        if errors:
            extra_fields["errors"] = errors

        body = body_maker.to_dict(**extra_fields, **kwargs)

        final_status = status_code or body_maker.get_status_code()

        logger.warning(
            f"Error response: {message_key}",
            extra={"errors": errors, "context": context}
        )

        return Response(body, status=final_status)

    @staticmethod
    def validation_error(
        errors: Dict[str, Any],
        request: Request = None,
        message_key: str = "VALIDATION_ERROR",
        context: Dict[str, Any] = None,
        **kwargs
    ) -> Response:
        return CustomResponse.error(
            message_key=message_key,
            request=request,
            context=context,
            errors=errors,
            status_code=400,
            **kwargs
        )

    @staticmethod
    def not_found(
        message_key: str = "NOT_FOUND",
        request: Request = None,
        context: Dict[str, Any] = None,
        **kwargs
    ) -> Response:
        return CustomResponse.error(
            message_key=message_key,
            request=request,
            context=context,
            status_code=404,
            **kwargs
        )

    @staticmethod
    def unauthorized(
        message_key: str = "UNAUTHORIZED",
        request: Request = None,
        context: Dict[str, Any] = None,
        **kwargs
    ) -> Response:
        return CustomResponse.error(
            message_key=message_key,
            request=request,
            context=context,
            status_code=401,
            **kwargs
        )

    @staticmethod
    def forbidden(
        message_key: str = "PERMISSION_DENIED",
        request: Request = None,
        context: Dict[str, Any] = None,
        **kwargs
    ) -> Response:
        return CustomResponse.error(
            message_key=message_key,
            request=request,
            context=context,
            status_code=403,
            **kwargs
        )
