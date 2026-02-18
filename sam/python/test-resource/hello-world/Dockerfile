FROM public.ecr.aws/lambda/nodejs:24@sha256:2ae0aecfac970190fe1fa2f9de439fb35340d285eb29a715ce6daf18eda7f54c

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
