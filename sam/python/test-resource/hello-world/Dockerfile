FROM public.ecr.aws/lambda/nodejs:24@sha256:4416823b42dbae95550d1e76267e96948f297c3867a2def1c7ba069082f65fda

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
