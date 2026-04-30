FROM public.ecr.aws/lambda/nodejs:24@sha256:21037c34addbd5b4022199de8bf8af720a605379aab334d3a990ba6332aaff0b

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
