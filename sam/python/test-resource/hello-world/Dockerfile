FROM public.ecr.aws/lambda/nodejs:20@sha256:52d2f7257d6c8bb976b27def31a134224d6cc34376cc6fcab15c63cbc44406a4

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
