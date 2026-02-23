FROM public.ecr.aws/lambda/nodejs:24@sha256:c2d42760f10130c2615cb3ac1f54fe641aacb2e847a4f8aede34f47d1f61db1a

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
