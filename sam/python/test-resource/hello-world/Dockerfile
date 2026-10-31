FROM public.ecr.aws/lambda/nodejs:24@sha256:5cc37494661b4b8cad808eb78ce36737c9c96b6fcaf0b2af67c4df4f63aff0f9

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
