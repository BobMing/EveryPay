import sae
import os.path
import tornado.wsgi
import everypayServer

app = tornado.wsgi.WSGIApplication(
    handlers = [(r"/", everypayServer.MainHandler)],
    template_path=os.path.join(os.path.dirname(__file__), 'templates'),
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
    debug=True
)

application = sae.create_wsgi_app(app)