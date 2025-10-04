FROM public.ecr.aws/lambda/nodejs:20@sha256:bde208295ba06bdc57af8ce6ba74773ee3cd2eb75a17062ab41e0615d6814211

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
