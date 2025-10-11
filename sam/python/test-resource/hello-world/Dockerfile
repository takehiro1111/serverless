FROM public.ecr.aws/lambda/nodejs:20@sha256:21a3d337d99cb19c3114a688e1b878527d9131af43fbd5f98ce67c71da542712

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
