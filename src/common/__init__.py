from src.common.controller.controller import VControllerBase
from src.common.controller.rest_method import rest_route_decorator
from src.common.utils.xlog import XLogMixin

RestGet = rest_route_decorator(methods_default=['GET'])
RestPost = rest_route_decorator(methods_default=['POST'])
RestDelete = rest_route_decorator(methods_default=['DELETE'])
RestPut = rest_route_decorator(methods_default=['PUT'])
RestHead = rest_route_decorator(methods_default=['HEAD'])
RestConnect = rest_route_decorator(methods_default=['CONNECT'])
RestOptions = rest_route_decorator(methods_default=['OPTIONS'])
RestTrace = rest_route_decorator(methods_default=['TRACE'])
RestPatch = rest_route_decorator(methods_default=['PATCH'])
