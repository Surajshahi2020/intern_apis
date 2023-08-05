from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from common.serializer import (
    OperationError,
    OperationSuccess,
)
from common.pagination import CustomPagination
from common.permissions import (
    IsSupervisor,
    IsAuthenticated,
    IsIntern,
    IsInternOrSupervisor,
)
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiExample,
)
from internapp.api.serializers.accounts import (
    UserDetailSerializer,
    UserSerializer,
    LoginSerializer,
    TaskCreateSerializer,
    TaskEditSerializer,
    SubmitTaskListSerializer,
    SubmitTaskSerializer,
    SubmitTaskEditSerializer,
)
from internapp.models import (
    User,
    Task,
    SubmittedTask,
)
from common.utils import validate_uuid
from common.exceptions import UnprocessableEntityException


@extend_schema_view(
    post=extend_schema(
        summary="Refer to Schema At Bottom",
        examples=[
            OpenApiExample(
                name="Register as Intern",
                request_only=True,
                value={
                    "role": "I",
                    "email": "intern@example.com",
                    "password": "securepassword",
                    "full_name": "John Doe",
                    "phone": "1234567890",
                    "gender": "M",
                    "profile_pic": "string",
                    "date_of_birth": "1990-01-01",
                    "contact_details": "Contact details here",
                    "educational_background": "Educational background here",
                    "work_experience": "3",
                },
            ),
            OpenApiExample(
                name="Register as Supervisor",
                request_only=True,
                value={
                    "role": "S",
                    "email": "supervisor@example.com",
                    "password": "securepassword",
                    "full_name": "Jane Smith",
                    "phone": "9876543210",
                    "gender": "F",
                    "profile_pic": "string",
                    "date_of_birth": "1985-05-15",
                    "contact_details": "Contact details here",
                    "educational_background": "Educational background here",
                    "work_experience": "3",
                },
            ),
        ],
        description="Login Api",
        request=UserSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when user is registered successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["User Unauthenticated Apis"],
    ),
)
class UserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Accounts",
                "message": "Accounts created successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    post=extend_schema(
        summary="Refer to Schema At Bottom",
        examples=[
            OpenApiExample(
                name="Login by email-email",
                request_only=True,
                value={"email": "kingshahi163@gmail.com", "password": "HIGHspeed12@"},
            ),
            OpenApiExample(
                name="Login by phone-phone",
                request_only=True,
                value={
                    "phone": "9809461773",
                    "password": "HIGHspeed12@",
                },
            ),
        ],
        description="Login Api",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when Loggedin successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["User Unauthenticated Apis"],
    ),
)
class LoginViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if "email" in serializer.validated_data:
            user = User.objects.filter(email=serializer.validated_data["email"]).first()
        elif "phone" in serializer.validated_data:
            user = User.objects.filter(phone=serializer.validated_data["phone"]).first()
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        return Response(
            {
                "title": "Login",
                "message": "Logged in successfully",
                "data": {
                    **UserDetailSerializer(instance=user).data,
                    "access": str(access_token),
                    "refresh": str(refresh_token),
                },
            }
        )


@extend_schema_view(
    post=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Task Create Apis",
        request=TaskCreateSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when task is created successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Task Apis"],
    ),
)
class TaskCreateViewSet(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsSupervisor]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Task",
                "message": "Task created successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    get=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Task List Apis",
        request=TaskCreateSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when Task is listed successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Dashboard Apis[Supervisor/Intern]"],
    ),
)
class TaskListViewSet(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = [
        "get",
    ]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(creator=user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "Task",
                "message": "Task Listed successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    patch=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Task Edit Apis",
        request=TaskEditSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when Task is edited successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Task Apis"],
    ),
)
class TaskEditViewSet(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskEditSerializer
    permission_classes = [IsSupervisor]
    http_method_names = [
        "patch",
    ]

    def partial_update(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        if not validate_uuid(pk):
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Invalid UUID",
                },
                code=422,
            )
        if not Task.objects.filter(id=pk).exists():
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Task does  not exist!",
                },
                code=422,
            )
        response = super().partial_update(request, *args, **kwargs)
        return Response(
            {
                "title": "Task",
                "message": "Task edited successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    post=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Submit Task Apis",
        request=SubmitTaskSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when task is edited successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Intern Apis"],
    ),
)
class SubmitTaskViewSet(generics.CreateAPIView):
    queryset = SubmittedTask.objects.all()
    serializer_class = SubmitTaskSerializer
    permission_classes = [IsIntern]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "title": "Submit Task",
                "message": "Submit Task created successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    get=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Submit Task List Apis",
        request=SubmitTaskSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when Submitted Task is listed successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Intern Apis"],
    ),
)
class TaskSubmitListViewSet(generics.ListAPIView):
    queryset = SubmittedTask.objects.all()
    serializer_class = SubmitTaskListSerializer
    permission_classes = [IsInternOrSupervisor]
    http_method_names = [
        "get",
    ]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "Submit Task",
                "message": "Submit Task Listed successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    patch=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Submit Task Edit Apis",
        request=SubmitTaskEditSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when Submitted Task is edited successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Intern Apis"],
    ),
)
class SubmitTaskEditViewSet(generics.UpdateAPIView):
    queryset = SubmittedTask.objects.all()
    serializer_class = SubmitTaskEditSerializer
    permission_classes = [IsSupervisor]
    http_method_names = [
        "patch",
    ]

    def partial_update(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        if not validate_uuid(pk):
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Invalid UUID",
                },
                code=422,
            )
        if not SubmittedTask.objects.filter(id=pk).exists():
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Submit Task does  not exist!",
                },
                code=422,
            )
        response = super().partial_update(request, *args, **kwargs)
        return Response(
            {
                "title": "Submit Task",
                "message": "Submit Task edited successfully",
                "data": response.data,
            }
        )


@extend_schema_view(
    get=extend_schema(
        summary="Refer to Schemas At Bottom",
        description="Task List Apis",
        request=TaskCreateSerializer,
        responses={
            200: OpenApiResponse(
                response=OperationSuccess,
                description="Success Response when Task is listed successfully",
            ),
            422: OpenApiResponse(
                response=OperationError,
                description="Json Data Error, occurs when invalid data is sent!",
            ),
        },
        tags=["Dashboard Apis[Supervisor/Intern]"],
    ),
)
class TaskListInternViewSet(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = [
        "get",
    ]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(contributors=user, status__in=["D", "O"])

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "title": "Submitted Task",
                "message": "Submitted Task Listed successfully",
                "data": response.data,
            }
        )
