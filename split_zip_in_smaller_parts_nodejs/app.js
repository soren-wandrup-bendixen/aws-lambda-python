exports.handler = async (event) => {

// create readstreams for all the output files and store them
lReqFiles.forEach(function(tFileKey){
s3FileReadStreams.push({
"stream": UTIL_S3.S3.getObject({
Bucket: CFG.aws.s3.bucket,
Key: tFileKey
}).createReadStream(),
"filename": tFileKey
});
});
//
const Stream = STREAM.Stream;
const streamPassThrough = new Stream.PassThrough();
// Create a zip archive using streamPassThrough style for the linking request in s3bucket
outputFile = ${CFG.aws.s3.outputDir}/archives/${lReqId}.zip;
const params = {
ACL: 'private',
Body: streamPassThrough,
Bucket: CFG.aws.s3.bucket,
ContentType: 'application/zip',
Key: outputFile
};
const s3Upload = UTIL_S3.S3.upload(params, (err, resp) => {
if (err) {
console.error(Got error creating stream to s3 ${err.name} ${err.message} ${err.stack});
throw err;
}
console.log(resp);
}).on('httpUploadProgress', (progress) => {
console.log(progress); // { loaded: 4915, total: 192915, part: 1, key: 'foo.jpg' }
});
// create the archiver
const archive = Archiver('zip');
archive.on('error', (error) => {
throw new Error(${error.name} ${error.code} ${error.message} ${error.path} ${error.stack});
});
// connect the archiver to upload streamPassThrough and pipe all the download streams to it
await new Promise((resolve, reject) => {
console.log("Starting upload of the output Files Zip Archive");
//
s3Upload.on('close', resolve());
s3Upload.on('end', resolve());
s3Upload.on('error', reject());
//
archive.pipe(streamPassThrough);
s3FileReadStreams.forEach((s3FileDwnldStream) => {
archive.append(s3FileDwnldStream.stream, { name: s3FileDwnldStream.filename })
});
archive.finalize();
//
}).catch((error) => {
throw new Error(${error.code} ${error.message} ${error.data});
});
//
// Finally wait for the uploader to finish
await s3Upload.promise();
//



    // TODO implement
    const response = {
        statusCode: 200,
        body: JSON.stringify('Hello from Lambda!'),
    };
    return response;
};


 
