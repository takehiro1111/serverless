FROM public.ecr.aws/lambda/nodejs:20@sha256:279d3a74dd9b10402ac447199e50f6531076aaa9431760fb0ee1c4a1f856bb8d

COPY app.mjs package*.json ./

RUN npm install
# If you are building your code for production, instead include a package-lock.json file on this directory and use:
# RUN npm ci --production

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambdaHandler"]
