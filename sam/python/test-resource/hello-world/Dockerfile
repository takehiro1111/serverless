FROM public.ecr.aws/lambda/nodejs:20@sha256:71ba604ae68587787fe45566e6b4e739de7bde66ba7b43eb09102781c0b71b1d

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
