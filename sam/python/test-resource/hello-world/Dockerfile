FROM public.ecr.aws/lambda/nodejs:22@sha256:05162cf1801c3c496b31cef36bb985b0192ae3d19a20225a22512054d5ecffe9

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
