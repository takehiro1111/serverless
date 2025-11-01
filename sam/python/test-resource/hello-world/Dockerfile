FROM public.ecr.aws/lambda/nodejs:20@sha256:4a0564393dd4b27ea2a1eee7cf68908032a9d26c555011f1480066575e1fede6

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
