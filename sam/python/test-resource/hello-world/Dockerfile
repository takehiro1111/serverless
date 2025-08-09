FROM public.ecr.aws/lambda/nodejs:20@sha256:a30bb740cdb89824667227a5a4f5eba805558293ffad44530d5dbc25b41d32ca

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
