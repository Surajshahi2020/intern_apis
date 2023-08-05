from rest_framework import serializers

from internapp.models import (
    User,
    InternProfile,
    SupervisorProfile,
    Task,
    SubmittedTask,
)
from common.exceptions import UnprocessableEntityException
from common.utils import (
    validate_email,
    validate_password,
    validate_phone,
    validate_url,
    validate_uuid,
)


class UserDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("password", None)
        role = data.get("role")

        if role == "S":
            supervisor_profiles = SupervisorProfile.objects.filter(user=instance)
            if supervisor_profiles.exists():
                data["contact_details"] = supervisor_profiles.first().contact_details
                data[
                    "educational_background"
                ] = supervisor_profiles.first().educational_background
                data["work_experience"] = supervisor_profiles.first().work_experience

        elif role == "I":
            intern_profiles = InternProfile.objects.filter(user=instance)
            if intern_profiles.exists():
                data["contact_details"] = intern_profiles.first().contact_details
                data[
                    "educational_background"
                ] = intern_profiles.first().educational_background
                data["work_experience"] = intern_profiles.first().work_experience

        return data

    class Meta:
        model = User
        fields = [
            "id",
            "role",
            "full_name",
            "phone",
            "email",
            "password",
            "gender",
            "profile_pic",
            "date_of_birth",
            "profile_pic",
        ]

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance


class UserSerializer(serializers.ModelSerializer):
    contact_details = serializers.CharField(write_only=True)
    educational_background = serializers.CharField(write_only=True)
    work_experience = serializers.FloatField(write_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop("password", None)
        data["contact_details"] = instance.internprofile.contact_details
        data["educational_background"] = instance.internprofile.educational_background
        data["work_experience"] = instance.internprofile.work_experience

        return data

    class Meta:
        model = User
        fields = [
            "id",
            "role",
            "full_name",
            "phone",
            "email",
            "password",
            "gender",
            "profile_pic",
            "date_of_birth",
            "profile_pic",
            "contact_details",
            "educational_background",
            "work_experience",
        ]

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        work_experience = data.get("work_experience")
        if data.get("full_name") == "":
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "FullName is required fields!",
                }
            )

        if data.get("password") == "":
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Password is required fields!",
                }
            )

        if not validate_password(data.get("password")):
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character!",
                }
            )

        if not data.get("profile_pic") == "" and not validate_url(
            data.get("profile_pic")
        ):
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Valid profile picture is required!",
                }
            )

        if data.get("phone") == "":
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Phone is required field!",
                }
            )

        if data.get("email") == "":
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Emaul is required field!",
                }
            )

        if not data.get("phone") == "" and not validate_phone(data.get("phone")):
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Invalid phone number!",
                }
            )

        if not data.get("email") == "" and not validate_email(data.get("email")):
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Invalid email!",
                }
            )

        if data.get("work_experience") == "":
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "work_experience is required fields!",
                }
            )

        if User.objects.filter(phone=data.get("phone")).exists():
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Phone number already linked with another user!",
                },
            )

        if User.objects.filter(email=data.get("email")).exists():
            raise UnprocessableEntityException(
                {
                    "title": "Accounts",
                    "message": "Email already linked with another user!",
                },
            )
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        role = validated_data.get("role", None)
        password = validated_data.pop("password", None)

        contact_details = validated_data.pop("contact_details")
        educational_background = validated_data.pop("educational_background")
        work_experience = validated_data.pop("work_experience")

        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()

        if role == "I":
            InternProfile.objects.create(
                user=instance,
                contact_details=contact_details,
                educational_background=educational_background,
                work_experience=work_experience,
            )
        else:
            SupervisorProfile.objects.create(
                user=instance,
                contact_details=contact_details,
                educational_background=educational_background,
                work_experience=work_experience,
            )

        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    phone = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data

        if "phone" in data:
            if not data.get("phone") == "" and not validate_phone(data.get("phone")):
                raise UnprocessableEntityException(
                    {
                        "title": "Login",
                        "message": "Valid Phone is required!",
                    }
                )

        if "email" in data:
            if not data.get("email") == "" and not validate_email(data.get("email")):
                raise UnprocessableEntityException(
                    {
                        "title": "Login",
                        "message": "Valid Email is required!",
                    }
                )

        if data.get("password") == "":
            raise UnprocessableEntityException(
                {
                    "title": "Login",
                    "message": "Password is required field!",
                }
            )

        if "email" in data:
            user = User.objects.filter(email=data.get("email")).first()
        elif "phone" in data:
            user = User.objects.filter(phone=data.get("phone")).first()
        if user is not None:
            if user.check_password(data.get("password")):
                if user.is_blocked:
                    raise UnprocessableEntityException(
                        {
                            "title": "Login",
                            "message": "Account has been blocked!",
                        }
                    )
                if not user.is_active:
                    raise UnprocessableEntityException(
                        {
                            "title": "Login",
                            "message": "Account is not activated yet!",
                        }
                    )

            else:
                raise UnprocessableEntityException(
                    {
                        "title": "Login",
                        "message": "Incorrect Password!",
                    }
                )
        else:
            raise UnprocessableEntityException(
                {
                    "title": "Login",
                    "message": "Email or Phone does not exist!",
                }
            )
        return super().is_valid(raise_exception=raise_exception)


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "deadline",
            "contributors",
            "status",
            "creator",
        ]

        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "status": {
                "read_only": True,
            },
            "contributors": {
                "read_only": True,
            },
            "creator": {
                "read_only": True,
            },
        }

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        if data.get("title") == "" or data.get("title") is None:
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Title is required and cannot be empty.",
                }
            )

        if data.get("description") == "" or data.get("description") is None:
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Description is required and cannot be empty.",
                }
            )

        task = Task.objects.filter(title=data.get("title"))
        if task.exists():
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Title already exists.",
                }
            )

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = self.context["request"].user
        instance = super().create(validated_data)
        instance.creator = user
        instance.save()
        return instance


class TaskEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "contributors",
            "status",
        ]

        extra_kwargs = {
            "id": {
                "read_only": True,
            }
        }

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data

        if data.get("title") == "" or data.get("title") is None:
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Title is required and cannot be empty.",
                }
            )

        if data.get("description") == "" or data.get("description") is None:
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Description is required and cannot be empty.",
                }
            )

        if data.get("status") not in ["D", "O", "C"]:
            raise UnprocessableEntityException(
                {
                    "title": "Task",
                    "message": "Invalid status. Only D, O and C are acceptable.",
                }
            )

        for contributor in data.get("contributors", []):
            if not validate_uuid(contributor):
                raise UnprocessableEntityException(
                    {
                        "title": "Task",
                        "message": "Invalid contributor",
                    }
                )
            if not User.objects.filter(id=contributor).exists():
                raise UnprocessableEntityException(
                    {
                        "title": "Task",
                        "message": f"User with ID '{contributor}' does not exist.",
                    }
                )

        return super().is_valid(raise_exception=raise_exception)

    def update(self, instance, validated_data):
        contributors_data = validated_data.pop("contributors", [])
        task = super().update(instance, validated_data)
        for contributor_id in contributors_data:
            if contributor_id.role == "I":
                task.contributors.add(contributor_id)
            else:
                raise UnprocessableEntityException(
                    {
                        "title": "Task",
                        "message": f"User with ID '{contributor_id}' is not intern role.Ony Intern can be assigned task",
                    }
                )
        return task


class SubmitTaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedTask
        fields = "__all__"


class SubmitTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedTask
        fields = [
            "id",
            "task",
        ]

        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        if data.get("task") == "" or data.get("task") is None:
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Task is required and cannot be empty.",
                }
            )

        if not validate_uuid(data.get("task")):
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Invalid task.",
                }
            )

        task = Task.objects.filter(id=data.get("task"))
        if not task.exists():
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Task does not exist.",
                }
            )
        task = task.first()
        user = self.context["request"].user.id
        if user not in task.contributors.values_list("id", flat=True):
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Current user is not a contributor to this task",
                }
            )

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = self.context["request"].user
        task = validated_data.get("task")
        if SubmittedTask.objects.filter(creator=user, task=task).exists():
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Already submitted.",
                }
            )
        else:
            submitter = super().create(validated_data)
            submitter.creator = user
            submitter.save()
            return submitter


class SubmitTaskEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedTask
        fields = [
            "is_approved",
            "remarks",
            "score",
        ]
        depth = 1

    def is_valid(self, *, raise_exception=False):
        data = self.initial_data
        if data.get("score", None) > 10:
            raise UnprocessableEntityException(
                {
                    "title": "Submit Task",
                    "message": "Score should not be grater than 10",
                }
            )
        return super().is_valid(raise_exception=raise_exception)

    def update(self, instance, validated_data):
        validated_data["modifier"] = self.context["request"].user
        instance = super().update(instance, validated_data)
        instance.task.status = "O"
        instance.task.save()
        return instance
