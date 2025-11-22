FROM public.ecr.aws/lambda/nodejs:20@sha256:c2368071b0bab3c22b399638f9543a3355e8a821780b7d465cd826fa7700bf8e

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
