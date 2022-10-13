/** Functioning as of 10/12. Still outputs an unwanted header of "entries":[ ] at the start of output.
  * Added .filter() before map to to check & take ?state="" param. 
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
         
         function isState(row){
            if(params.dealerId && params.dealerId == row.doc.id){
                return row;
            } else if(params.state && params.state == row.doc.st){
                return row;
            } else if(!params.state && !params.dealerId){ 
                return row; 
            }
         }
         
         var dealerships = dbList.result.rows.filter(isState).map((row) => {
            return{
                row
                /*
                id: row.doc.id,
                city: row.doc.city,
                state: row.doc.state,
                st: row.doc.st,
                address: row.doc.address,
                zip: row.doc.zip,
                lat: row.doc.lat,
                long: row.doc.long,
                */
             }
             
         })
         
         return { 
            dealerships
         };
       } catch (error) {
           return { error: error.description };
       }
 }