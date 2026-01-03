FROM public.ecr.aws/lambda/nodejs:20@sha256:c9db858f1061d1662d081a7d3fe30e1c9cf8dd4eb658f60ab34cc8ebe8f939a0

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
