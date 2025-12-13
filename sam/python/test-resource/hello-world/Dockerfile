FROM public.ecr.aws/lambda/nodejs:20@sha256:4075ea2d4734de1cb8be471fcca3a14622d57e1a83f4cd36fa54d814e268152c

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
