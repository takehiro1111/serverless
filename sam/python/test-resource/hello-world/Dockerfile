FROM public.ecr.aws/lambda/nodejs:22@sha256:a902ed0cffd6ec67cfa4c6ec4e8d6f754179ab3eb35d19d18b45864db431e214

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
