"""
Manage the environment when python is using mod_python
"""

from mod_python import util

from chula.www.adapters import env

class Environment(env.BaseEnv):
    def __init__(self, req):
        super(Environment, self).__init__()

        # Expose access to additional mod_python environment variables
        req.add_common_vars()
        subprocess = req.subprocess_env.copy()

        # Set the required variables from mod_python's req object(s)
        for key, value in req.subprocess_env.copy().iteritems():
            key = key.replace('.', '_')
            if key in self:
                self[key] = value
            
        # Add environment variables not available in subprocess_env
        self.PATH_INFO = req.path_info

        # If req.form exists and is of type util.FieldStorage use it,
        # else use what mod_python publisher would use.
        try:
            if isinstance(self.req.form, util.FieldStorage):
                pass
        except:
            self.form = util.FieldStorage(req, keep_blank_values=1)

        # Add additional variables provided by the base class
        super(Environment, self).extras()
