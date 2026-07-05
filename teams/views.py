from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TeamCreateSerializer, TeamDetailSerializer
from .models import Team, TeamMembership
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

class TeamViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Team.objects.filter(members__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return TeamCreateSerializer
        return TeamDetailSerializer
    
    
    def perform_create(self, serializer):
        team = serializer.save(created_by=self.request.user)
        TeamMembership.objects.create(team=team, user=self.request.user, role='owner', )

class TeamMemberViewset(viewsets.ModelViewSet):
    def get_queryset(self):
        team_id = self.kwargs["pk"]
        team = get_object_or_404(Team, id=team_id)
        if not team.members.filter(user=self.request.user).exists():
            raise PermissionDenied("You're not a member of this team")
        return team.members.all()