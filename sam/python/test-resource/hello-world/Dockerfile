FROM public.ecr.aws/lambda/nodejs:22@sha256:3289a8e9f108906b9267cc91e79c4c6f1533428d2776c8eb30b7a6cd88a180cc

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
