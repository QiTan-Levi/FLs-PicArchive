// 创建文件存储集合
db.createCollection("files", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["filename", "contentType", "uploadDate", "length"],
            properties: {
                filename: { bsonType: "string" },
                contentType: { bsonType: "string" },
                uploadDate: { bsonType: "date" },
                length: { bsonType: "long" },
                chunkSize: { bsonType: "int" },
                metadata: {
                    bsonType: "object",
                    properties: {
                        fileType: { bsonType: "string", enum: ["avatar", "image"] },
                        originalName: { bsonType: "string" },
                        width: { bsonType: "int" },
                        height: { bsonType: "int" },
                        size: { bsonType: "int" }
                    }
                }
            }
        }
    }
});

// 创建文件块集合
db.createCollection("chunks", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["files_id", "n", "data"],
            properties: {
                files_id: { bsonType: "objectId" },
                n: { bsonType: "int" },
                data: { bsonType: "binData" }
            }
        }
    }
});

// 创建索引
db.files.createIndex({ filename: 1 });
db.files.createIndex({ uploadDate: -1 });
db.files.createIndex({ "metadata.fileType": 1 });

db.chunks.createIndex({ files_id: 1, n: 1 }, { unique: true });