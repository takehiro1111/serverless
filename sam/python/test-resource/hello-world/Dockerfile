FROM public.ecr.aws/lambda/nodejs:20@sha256:f687f5d21896f9af091d1f9d715bea1503e8f68c2986559a025b49fb238e738a

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
