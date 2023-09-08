German-English dictionary (FastAPI + Redis + Dependency Injector + HTMX)
=============================================

This is a dummy app based on `FastAPI <https://docs.python.org/3/library/asyncio.html>`_
+ `Redis <https://redis.io/>`_
+ `Dependency Injector <https://python-dependency-injector.ets-labs.org/>`_
+ `HTMX <https://htmx.org//>`_.

On load the dictionary is loaded into redis and local trie for typeahead is built.
When using typeahead the requests are executed on '/search', on submit the app
tries to get the corresponding dictionary article from redis.

Run
---

Build the Docker image:

.. code-block:: bash

   docker-compose build

Run the docker-compose environment:

.. code-block:: bash

    docker-compose up