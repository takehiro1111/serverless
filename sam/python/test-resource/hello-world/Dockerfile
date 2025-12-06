FROM public.ecr.aws/lambda/nodejs:24@sha256:a65fcd88ce68644764f7f937460a18e4d97bb3ac60359a83266cd8cc1ced322b

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
