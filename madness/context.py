
from werkzeug.local import Local, LocalManager, LocalProxy, LocalStack

local = Local()
local_manager = LocalManager([local])
request = local('request')
context = local('context')
