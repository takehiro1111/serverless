FROM public.ecr.aws/lambda/nodejs:20@sha256:4755182a6b9bbb8d713cb585038a8c100012c03fde73af4136e97ff0506f9f16

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
