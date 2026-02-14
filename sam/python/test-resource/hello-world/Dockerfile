FROM public.ecr.aws/lambda/nodejs:20@sha256:ae519cb4eac234af304e64f92e0fb003f9d8a44d81204080412500918fc89c18

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
