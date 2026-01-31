FROM public.ecr.aws/lambda/nodejs:20@sha256:b240103d428d50a293f24d428548f55a556b7763f944998ce94e32d230ddbaa8

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
