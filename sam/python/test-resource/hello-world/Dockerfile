FROM public.ecr.aws/lambda/nodejs:22@sha256:c392bc926ee10208904a5c0f655c1235faa24b5eae7e59c9b92aaa2931f95854

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
