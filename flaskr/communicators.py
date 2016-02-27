"""Concrete implementations of communicators for various API endpoints. These
   are equivalent to servlets in Java"""

# imports
import base_communicator
import handlers
import errors
import service_objects


class ComparisonWithFriendsServlet(base_communicator.BaseCommunicator, object):
    """
    Servlet
    """

    def __init__(self):
        super(ComparisonWithFriendsServlet, self).__init__()

    def invoke_fetch(self, request):
        raise errors.FunctionalityNotImplemented()

    def invoke_insert(self, request):
        """Corresponds to post method. Gets the actual flask request object in
         input"""
        # First fetch input data from the request
        request_data = super(ComparisonWithFriendsServlet,
                             self).get_request_data(request)
        # Check auth
        auth_res = super(ComparisonWithFriendsServlet, self).check_auth(request_data,
                                                                        request)
        if auth_res:
            # First create a service object for this
            self_name = self.__class__.__name__
            class_name = self_name.replace("Servlet", "")
            if request_data['type'] == 'ComparisonWithFriendsServlet':
                svc_obj = service_objects.ComparisonWithFriends(request_data)
            handler_inst = handlers.HandlerFactory.get_handler(class_name)
            res_data = handler_inst.get(svc_obj)
        else:
            raise errors.CouldNotAuthenticate()
        resp = super(ComparisonWithFriendsServlet, self).get_response(res_data)
        return resp


class UsersListServlet(base_communicator.BaseCommunicator, object):
    """
    Servlet
    """

    def __init__(self):
        super(UsersListServlet, self).__init__()

    def invoke_fetch(self, request):
        raise errors.FunctionalityNotImplemented()

    def invoke_insert(self, request):
        """Corresponds to post method. Gets the actual flask request object in
         input"""
        # First fetch input data from the request
        request_data = super(UsersListServlet,
                             self).get_request_data(request)
        # Check auth
        auth_res = super(UsersListServlet, self).check_auth(request_data,
                                                            request)
        if auth_res:
            # First create a service object for this
            self_name = self.__class__.__name__
            class_name = self_name.replace("Servlet", "")
            svc_obj = getattr(service_objects, class_name)(request_data)
            handler_inst = handlers.HandlerFactory.get_handler(class_name)
            res_data = handler_inst.get(svc_obj)
        else:
            print "testing"
            raise errors.CouldNotAuthenticate()
        # Create response object
        resp = super(UsersListServlet, self).get_response(res_data)
        return resp


class FriendRequestActionServlet(base_communicator.BaseCommunicator, object):
    """
    Servlet
    """

    def __init__(self):
        super(FriendRequestActionServlet, self).__init__()

    def invoke_fetch(self, request):
        raise errors.FunctionalityNotImplemented()

    def invoke_insert(self, request):
        """Corresponds to post method. Gets the actual flask request object in
         input"""
        # First fetch input data from the request
        request_data = super(FriendRequestActionServlet,
                             self).get_request_data(request)
        # Check auth
        auth_res = super(FriendRequestActionServlet, self).check_auth(request_data,
                                                                      request)
        if auth_res:
            # First create a service object for this
            self_name = self.__class__.__name__
            class_name = self_name.replace("Servlet", "")
            svc_obj = getattr(service_objects, class_name)(request_data)
            handler_inst = handlers.HandlerFactory.get_handler(class_name)
            res_data = handler_inst.get(svc_obj)
        else:
            print "testing"
            raise errors.CouldNotAuthenticate()
        # Create response object
        resp = super(FriendRequestActionServlet, self).get_response(res_data)
        return resp


class AddFriendServlet(base_communicator.BaseCommunicator, object):
    """
    Servlet
    """

    def __init__(self):
        super(AddFriendServlet, self).__init__()

    def invoke_fetch(self, request):
        raise errors.FunctionalityNotImplemented()

    def invoke_insert(self, request):
        """Corresponds to post method. Gets the actual flask request object in
         input"""
        # First fetch input data from the request
        request_data = super(AddFriendServlet,
                             self).get_request_data(request)
        # Check auth
        auth_res = super(AddFriendServlet, self).check_auth(request_data,
                                                            request)
        if auth_res:
            # First create a service object for this
            self_name = self.__class__.__name__
            class_name = self_name.replace("Servlet", "")
            svc_obj = getattr(service_objects, class_name)(request_data)
            handler_inst = handlers.HandlerFactory.get_handler(class_name)
            res_data = handler_inst.get(svc_obj)
        else:
            raise errors.CouldNotAuthenticate()
        # Create response object
        resp = super(AddFriendServlet, self).get_response(res_data)
        return resp


class FriendsFeedServlet(base_communicator.BaseCommunicator, object):
    """
    Servlet
    """

    def __init__(self):
        super(FriendsFeedServlet, self).__init__()

    def invoke_fetch(self, request):
        raise errors.FunctionalityNotImplemented()

    def invoke_insert(self, request):
        """Corresponds to post method. Gets the actual flask request object in
         input"""
        # First fetch input data from the request
        request_data = super(FriendsFeedServlet,
                             self).get_request_data(request)
        # Check auth
        auth_res = super(FriendsFeedServlet, self).check_auth(request_data,
                                                              request)
        if auth_res:
            # First create a service object for this
            self_name = self.__class__.__name__
            class_name = self_name.replace("Servlet", "")
            svc_obj = getattr(service_objects, class_name)(request_data)
            handler_inst = handlers.HandlerFactory.get_handler(class_name)
            res_data = handler_inst.get(svc_obj)
        else:
            raise errors.CouldNotAuthenticate()
        # Create response object
        resp = super(FriendsFeedServlet, self).get_response(res_data)
        return resp


class UpdateInfoServlet(base_communicator.BaseCommunicator, object):
    """Servelet
    """

    def __init__(self):
        """
        Calls init of super class
        """
        super(UpdateInfoServlet, self).__init__()

    def invoke_fetch(self, request):
        raise errors.FunctionalityNotImplemented()

    def invoke_insert(self, request):
        """Corresponds to post method. Gets the actual flask request object in
         input"""
        # First fetch input data from the request
        request_data = super(UpdateInfoServlet,
                             self).get_request_data(request)
        # Check auth
        auth_res = super(UpdateInfoServlet, self).check_auth(request_data
                                                             , request)
        if auth_res:
            # First create a service object for this
            self_name = self.__class__.__name__
            class_name = self_name.replace("Servlet", "")
            svc_obj = getattr(service_objects, class_name)(request_data)
            handler_inst = handlers.HandlerFactory.get_handler(class_name)
            res_data = handler_inst.get(svc_obj)
        else:
            raise errors.CouldNotAuthenticate()
        # Create response object
        resp = super(UpdateInfoServlet, self).get_response(res_data)
        return resp

class UserFeedServlet(base_communicator.BaseCommunicator, object):
    """Servelet
    """

    def __init__(self):
        """
        Calls init of super class
        """
        super(UserFeedServlet, self).__init__()

    def invoke_fetch(self, request):
        raise errors.FunctionalityNotImplemented()

    def invoke_insert(self, request):
        """Corresponds to post method. Gets the actual flask request object in
         input"""
        # First fetch input data from the request
        request_data = super(UserFeedServlet,
                             self).get_request_data(request)
        # Check auth
        auth_res = super(UserFeedServlet, self).check_auth(request_data
                                                             , request)
        if auth_res:
            # First create a service object for this
            self_name = self.__class__.__name__
            class_name = self_name.replace("Servlet", "")
            svc_obj = getattr(service_objects, class_name)(request_data)
            handler_inst = handlers.HandlerFactory.get_handler(class_name)
            res_data = handler_inst.get(svc_obj)
        else:
            raise errors.CouldNotAuthenticate()
        # Create response object
        resp = super(UserFeedServlet, self).get_response(res_data)
        return resp
