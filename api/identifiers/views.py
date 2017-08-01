from rest_framework import generics, permissions as drf_permissions

from framework.auth.oauth_scopes import CoreScopes

from api.base import permissions as base_permissions
from api.base.views import JSONAPIBaseView
from api.base.filters import ListFilterMixin
from api.base.serializers import JSONAPISerializer

from api.identifiers.serializers import NodeIdentifierSerializer, RegistrationIdentifierSerializer, PreprintIdentifierSerializer

from api.nodes.permissions import (
    IsPublic,
    ExcludeWithdrawals,
)

from osf.models import Node, Registration, PreprintService, Identifier


class IdentifierList(JSONAPIBaseView, generics.ListAPIView, ListFilterMixin):
    """List of identifiers for a specified node. *Read-only*.

    ##Identifier Attributes

    OSF Identifier entities have the "identifiers" `type`.

        name           type                   description
        ----------------------------------------------------------------------------
        category       string                 e.g. 'ark', 'doi'
        value          string                 the identifier value itself

    ##Links

        self: this identifier's detail page

    ##Relationships

    ###Referent

    The identifier is refers to this node.

    ##Actions

    *None*.

    ##Query Params

     Identifiers may be filtered by their category.

    #This Request/Response

    """

    permission_classes = (
        IsPublic,
        drf_permissions.IsAuthenticatedOrReadOnly,
        base_permissions.TokenHasScope,
        ExcludeWithdrawals
    )

    required_read_scopes = [CoreScopes.IDENTIFIERS_READ]
    required_write_scopes = [CoreScopes.NULL]

    view_category = 'identifiers'
    view_name = 'identifier-list'

    ordering = ('-id',)

    def get_object(self, *args, **kwargs):
        raise NotImplementedError

    def get_default_queryset(self):
        obj = self.get_object()
        if isinstance(obj, PreprintService):
            return obj.node.identifiers.all()
        return obj.identifiers.all()

    # overrides ListCreateAPIView
    def get_queryset(self):
        return self.get_queryset_from_request()


class IdentifierDetail(JSONAPIBaseView, generics.RetrieveAPIView):
    """List of identifiers for a specified node. *Read-only*.


    ##Identifier Attributes

    OSF Identifier entities have the "identifiers" `type`.

        name           type                   description
        ----------------------------------------------------------------------------
        category       string                 e.g. 'ark', 'doi'
        value          string                 the identifier value itself

    ##Links

        self: this identifier's detail page

    ##Relationships

    ###Referent

    The identifier is refers to this node.


    #This Request/Response

    """
    permission_classes = (
        drf_permissions.IsAuthenticatedOrReadOnly,
        base_permissions.TokenHasScope
    )

    required_read_scopes = [CoreScopes.IDENTIFIERS_READ]
    required_write_scopes = [CoreScopes.NULL]

    serializer_class = RegistrationIdentifierSerializer
    view_category = 'identifiers'
    view_name = 'identifier-detail'

    def get_serializer_class(self):
        if 'identifier_id' in self.kwargs:
            referent = self.get_object().referent
            if isinstance(referent, Node):
                return NodeIdentifierSerializer
            if isinstance(referent, Registration):
                return RegistrationIdentifierSerializer
            if isinstance(referent, PreprintService):
                return PreprintIdentifierSerializer
        return JSONAPISerializer

    def get_object(self):
        return Identifier.load(self.kwargs['identifier_id'])
