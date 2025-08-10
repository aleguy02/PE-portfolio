# Production Engineering - Week 1 - Portfolio Site

## Quickstart

This site uses a microservice architecture to handle the backend and database (and reverse-proxy in production).  
To run the application in development do `docker compose -f compose.yaml up -d` and to stop the application do `docker compose -f compose.yaml down -d`.  
To run the application in a production-level network do `docker compose -f compose.prod.yaml up -d`. Hopefully you won't have to stop the application manually.  

---

## Scripts

There are a few scripts in the scripts/ directory to aid in development and deployment. curl-test.sh is to test the timeline posts API and run-tests.sh is to, well, run tests. redeploy-site.sh is meant to be run in the VPS hosting the application. Read each script to learn more.

---

## TDD

This project follows the TDD (Test Driven Development) paradigm. Writing tests in parallel to development of a new feature is strongly encouraged. Writing tests when you encounter a bug is a must. Currently, unittest and pytest are the frameworks of choice. See scripts/run-tests.sh for more information/hint on how to run tests.
