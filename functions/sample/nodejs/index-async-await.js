/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);
      try {
        let dbList = await cloudant.getAllDbs();
        return { "dbs": dbList.result };
      } catch (error) {
          return { error: error.description };
      }
}



entries: dbList.rows.map((row) => { return {
  id: row.doc._id,
  city: row.doc.city,
  state: row.doc.state,
  st: row.doc.st,
  address: row.doc.address,
  zip: row.doc.zip,
  lat: row.doc.lat,
  long: row.doc.long,
}})

const tempArr = dbList.result.doc.map((doc) => {
  tempObj = {
      "id" : doc.id,
      "city" : doc.city,
      "state" : doc.state,
      "st" : doc.st,
      "address" : doc.address,
      "zip" : doc.zip,
      "lat" : doc.lat,
      "long" : doc.long,
  };
  
  data.push(tempObj);
  
  return{}
});



/////////////////// WORKING /////////////////////////
/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
 const { CloudantV1 } = require('@ibm-cloud/cloudant');
 const { IamAuthenticator } = require('ibm-cloud-sdk-core');
 
 async function main(params) {
       const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
       const cloudant = CloudantV1.newInstance({
           authenticator: authenticator
       });
       
       cloudant.setServiceUrl(params.COUCH_URL);
       
       try {
         let dbList = await cloudant.postAllDocs({
             db: 'dealerships',
             includeDocs: true,
         });
         
         if (params.state || !params.comment) {
             return Promise.reject({ error: 'no name or comment'});
         }
         
         return { 
             entries: dbList.result.rows.map((row) => { return{
                  id: row.doc.id,
                 city: row.doc.city,
                 state: row.doc.state,
                 st: row.doc.st,
                 address: row.doc.address,
                 zip: row.doc.zip,
                 lat: row.doc.lat,
                 long: row.doc.long,
              }})
 
         };
       } catch (error) {
           return { error: error.description };
       }
 }