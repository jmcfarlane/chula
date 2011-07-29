:mod:`chula.www.adapters.env` -- HTTP environment
=================================================

.. index::
   single: env
   pair: base; env

.. automodule:: chula.www.adapters.env

.. autoclass:: chula.www.adapters.env.BaseEnv
   :members:

   .. attribute:: CONTENT_LENGTH

      Document length.

   .. attribute:: DOCUMENT_ROOT

      Document root accordng to the web server.

   .. attribute:: GATEWAY_INTERFACE

      CGI version.

   .. attribute:: HTTP_ACCEPT

      http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html

   .. attribute:: HTTP_ACCEPT_CHARSET

      Accepted character sets.

   .. attribute:: HTTP_ACCEPT_ENCODING

      The MIME types the requestor will accept as defined in the HTTP
      header e.g.

   .. attribute:: HTTP_ACCEPT_LANGUAGE

      Retrieves a list of ISO languages that are set for the browser.

   .. attribute:: HTTP_CONNECTION

      The type of connection as defined in the HTTP header.

   .. attribute:: HTTP_COOKIE

      The value of any cookie in the HTTP header. Standard cookie
      formats are defined by RFC 2965 (Set-Cookie2 header).

   .. attribute:: HTTP_HOST

      The base URL of the host.

   .. attribute:: HTTP_KEEP_ALIVE

      Document...


   .. attribute:: HTTP_USER_AGENT

      The browser id or user-agent string identifying the browser
      (nominally defined by RFC 1945 and RFC 2068).

   .. attribute:: PATH

      Operating system :envvar:`PATH` as seen by the web server.

   .. attribute:: PATH_INFO

      The extra path information followin the script's path in the URL.

      Example: ``/foo/bar/``

   .. attribute:: QUERY_STRING

      Contains query information passed via the calling URL, following
      a question mark after the script location.

      Example: ``foo=bar&color=purple``

   .. attribute:: REMOTE_ADDR

      The IP address from which the client is issuing the request.

   .. attribute:: REMOTE_HOST

      The name of the host from which the client issues the request.

   .. attribute:: REMOTE_PORT


      The port of the host from which the client issues the request.

   .. attribute:: REQUEST_METHOD

      The method used for the request.

      Usually ``GET``, ``POST``, ``PUT`` or ``HEAD``

   .. attribute:: REQUEST_URI

      The URI for this request (relative to DOCUMENT_ROOT).

      Example: ``/foo/bar/?foo=bar&color=purple``

   .. attribute:: SCRIPT_FILENAME

      The path to the script being executed.

   .. attribute:: SCRIPT_NAME

      The file name of the script being executed (relative to DOCUMENT_ROOT).

   .. attribute:: SERVER_ADDR

      The IP address of the server for this URL.

   .. attribute:: SERVER_ADMIN

      The administrators e-mail address for this SERVER_NAME.

   .. attribute:: SERVER_NAME

      The servers host name, DNS alias or IP address.

   .. attribute:: SERVER_PORT

      The port number on this server to which this request was directed.

   .. attribute:: SERVER_PROTOCOL

      The name and revision of the protocol that delivered the current
      request.

   .. attribute:: SERVER_SIGNATURE

      The HTML string that may be embedded in the page to identify
      this host.

   .. attribute:: SERVER_SOFTWARE

      The name and version of the information server answering the query.

   .. attribute:: chula_adapter

      The type of adapter being used to fascilitate communication
      between the Chula application and the server.  Possible values
      are:

      #. ``FCGI/WSGI``
      #. ``MOD_PYTHON``
      #. ``WSGI``

   .. attribute:: chula_class

      The Python class to which this request was directed.

   .. attribute:: chula_method

      The Python method to which this request was directed.

   .. attribute:: chula_module

      The Python module to which this request was directed.

   .. attribute:: chula_package

      The Python package to which this request was directed.

   .. attribute:: chula_version

      The version of Chula which serviced this request.

   .. attribute:: wsgi_errors

        An output stream (file-like object) to which error output can
        be written, for the purpose of recording program or other
        errors in a standardized and possibly centralized location.
        This should be a "text mode" stream; i.e., applications should
        use "\n" as a line ending, and assume that it will be
        converted to the correct line ending by the server/gateway.

        For many servers, wsgi.errors will be the server's main error
        log.  Alternatively, this may be sys.stderr, or a log file of
        some sort. The server's documentation should include an
        explanation of how to configure this or where to find the
        recorded output. A server or gateway may supply different
        error streams to different applications, if this is desired.

    .. attribute:: wsgi_file_wrapper

         A callable that accepts one required positional parameter,
         and one optional positional parameter. The first parameter is
         the file-like object to be sent, and the second parameter is
         an optional block size "suggestion" (which the server/gateway
         need not use). The callable must return an iterable object,
         and must not perform any data transmission until and unless
         the server/gateway actually receives the iterable as a return
         value from the application. (To do otherwise would prevent
         middleware from being able to interpret or override the
         response data.)

    .. attribute:: wsgi_input

        An input stream (file-like object) from which the HTTP request
        body can be read. (The server or gateway may perform reads
        on-demand as requested by the application, or it may pre- read
        the client's request body and buffer it in-memory or on disk,
        or use any other technique for providing such an input stream,
        according to its preference.)

    .. attribute:: wsgi_multiprocess

        This value should evaluate true if an equivalent application
        object may be simultaneously invoked by another process, and
        should evaluate false otherwise.

    .. attribute:: wsgi_multithread

        This value should evaluate true if the application object may
        be simultaneously invoked by another thread in the same
        process, and should evaluate false otherwise.

    .. attribute:: wsgi_run_once

        This value should evaluate true if the server or gateway
        expects (but does not guarantee!) that the application will
        only be invoked this one time during the life of its
        containing process. Normally, this will only be true for a
        gateway based on CGI (or something similar).

    .. attribute:: wsgi_url_scheme

        A string representing the "scheme" portion of the URL at which
        the application is being invoked. Normally, this will have the
        value "http" or "https", as appropriate.

    .. attribute:: wsgi_version

        The :class:`tuple` ``(1, 0)``, representing WSGI version 1.0.

    .. attribute:: ajax_uri

        The HTTP protocol (taking into consideration SSL) and matching
        domain name used on this request.  This variable can be used
        when authoring javascript ajax requests that must match the
        domain exactly, so as to honor XSS rules.

    .. attribute:: content_type

        The value in the ``Content-Type`` HTTP header sent with this
        request.

    .. attribute:: cookies

        Cookies sent to the browser with this request, of type
        :class:`str`.

    .. attribute:: debug

        The value currently set for :attr:`chula.config.Config.debug`.

    .. attribute:: form

        :class:`dict` holding both HTTP GET and POST variables,
        with POST taking precidence if a key is in both.

    .. attribute:: form_get

        :class:`dict` holding HTTP GET values.

    .. attribute:: form_post

        :class:`dict` holding HTTP POST values.

    .. attribute:: form_raw

        :class:`str` holding raw payload (typically json or
        xml) if received.

    .. attribute:: form_rest

        :class:`dict` holding any key/value pairs defined in a regex
        mapper.

    .. attribute:: headers

        :class:`list` of :class:`dict` objects to be sent as HTTP
        headers for this request.

    .. attribute:: route

        :class:`dict` holding the Chula route information.  This is
        the collection that holds the package, module, class, and
        method routing destination.

    .. attribute:: status

        HTTP status code.

    .. attribute:: under_construction

        :class:`bool` indicating if the application is currently under
        construction.  See
        :attr:`chula.config.Config.construction_controller` for
        detail.

