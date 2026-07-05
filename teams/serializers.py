from rest_framework import serializers
from .models import Team, TeamMembership
from users.serializers import UserMiniSerializer



class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["name"]

class TeamDetailSerializer(serializers.ModelSerializer):
    created_by = UserMiniSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = "__all__"

    def get_member_count(self, obj):
        return obj.members.count()
    
class TeamMemberShipSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer()
    class Meta:
        model = TeamMembership
        fields = "__all__"

