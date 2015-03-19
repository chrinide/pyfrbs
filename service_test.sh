#!/usr/bin/env bash

if curl -s -i http://127.0.0.1:5000/api/variables | grep '200 OK' >/dev/null; then
	echo PASSED
else
	echo FAILED
fi

if curl -s -i http://127.0.0.1:5000/api/variables/1 | grep '200 OK' >/dev/null; then
	echo PASSED
else
	echo FAILED
fi

if curl -s -i http://127.0.0.1:5000/api/variables/2 | grep '200 OK' >/dev/null; then
	echo PASSED
else
	echo FAILED
fi

if curl -s -i http://127.0.0.1:5000/api/variables/3 | grep '200 OK' >/dev/null; then
	echo PASSED
else
	echo FAILED
fi

if curl -s -i http://127.0.0.1:5000/api/variables/4 | grep '404 NOT FOUND' >/dev/null; then
	echo PASSED
else
	echo FAILED
fi
