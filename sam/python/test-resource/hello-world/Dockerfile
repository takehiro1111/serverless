FROM public.ecr.aws/lambda/nodejs:24@sha256:81d4c138e7f000f998c3e29c81b7df9532251d2460e44040aa614021ed693d58

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
