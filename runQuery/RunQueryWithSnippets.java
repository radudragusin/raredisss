import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import au.com.bytecode.opencsv.CSVWriter;

import com.google.gson.Gson;

import lemurproject.indri.ParsedDocument;
import lemurproject.indri.QueryAnnotation;
import lemurproject.indri.QueryEnvironment;
import lemurproject.indri.ScoredExtentResult;

public class RunQueryWithSnippets {
	
	// Setup a profile
	static RetrievalProfileX profile;
	
	// Initialize the structures for the queries
	static List<String> queriesText = new ArrayList<String>();
	static List<String> queriesNames = new ArrayList<String>();
	
	/** You can call RunQuery with:
	 * - no argument -> will use default param file
	 * - one argument -> the parameter file to use (give path to file)
	 * - three arguments: the query, the collection, the output filename (path remains the same)
	 *    -> for the rest of the settings, use default param file
	*/ 
	
	public static void main( String[] args ) throws Exception {
		QueryEnvironment env = new QueryEnvironment();
		ScoredExtentResult[] results;
		QueryAnnotation annot;
		String[] docnos;
		String[] titles;
		ParsedDocument[] docs;
		ArrayList<String> snippets = new ArrayList<String>();
		
		String paramFile;
		String defaultParamFile = "retrieval_param.json";
		
		if(args.length == 0 || (args.length == 1 && args[0].endsWith(".json"))){
			if(args.length == 0){
				// Use default parameter file if none is given
				paramFile = defaultParamFile;
			}else{
				// Use given parameter file
				paramFile = args[0];
			}
			
			String json = readFileAsString(paramFile);
			profile = new Gson().fromJson(json, RetrievalProfileX.class);
			
			// Read the queries from file
			readQueries(profile.getQueryPath()+profile.getQueryFile());
			
		}else if (args.length == 3){
			//Use the given query, the given collection, and the default param file
			paramFile = defaultParamFile;
			
			String json = readFileAsString(paramFile);
			profile = new Gson().fromJson(json, RetrievalProfileX.class);
			
			String query = args[0];
			query = processQuery(query);
			
			queriesText.add(query);
			queriesNames.add(query);
			
			profile.setIndexName(args[1]);
			
			profile.setResultName(args[2]);
		}
		
		// Open an Indri repository
		env.addIndex(profile.getIndexPath()+profile.getIndexName());
		
		String[] rules = new String[1];
		rules[0] = profile.getRule();
		env.setScoringRules(rules);
		env.setMemory(Long.parseLong(profile.getMemory()));
		String query;
		String queryName;
				
		// Run the queries
		for(int q=0;q<queriesText.size();q++){
			query = queriesText.get(q);
			queryName = queriesNames.get(q);
			
			System.out.println("Running the query: "+query);
			
			// Run an Indri query, returning the specified nr of results
			//results = env.runQuery(query, Integer.parseInt(profile.getNrResults()));
			annot = env.runAnnotatedQuery(query, Integer.parseInt(profile.getNrResults()));
			results = annot.getResults();
			
			// Fetch relevant fields of the retrieved documents 
			docnos = env.documentMetadata(results, "docno");
			titles = env.documentMetadata(results, "title");
			docs = env.documents(results);
			snippets.clear();
			for(int j=0; j<docnos.length; j++){
				String snippet = SnippetBuilder.buildSnippet(annot,Integer.parseInt(docnos[j]),docs[j].text,docs[j].positions,100,10,100);
				snippets.add(snippet);
				//System.out.println(snippet);
			}
			
			writeToCsv(profile.getResultPath()+profile.getResultName(),queryName,results,docnos,titles,docs,snippets);
			System.out.println("Results saved in "+profile.getResultName());
		}

		env.close();
	}
	
	/**
	 * Read the parameter file (json format) and return its content as a string
	 */
	private static String readFileAsString(String filePath) throws java.io.IOException{
	    byte[] buffer = new byte[(int) new File(filePath).length()];
	    FileInputStream f = new FileInputStream(filePath);
	    f.read(buffer);
	    String fileContent = new String(buffer);
	    f.close();
	    return fileContent;
	}
	
	/**
	 * Read queries from file (one query per line, consisting of an identifier and the text of the query)
	 */
	public static void readQueries(String queriesFilePath) throws FileNotFoundException{
		Scanner scanner = new Scanner(new FileInputStream(queriesFilePath), "UTF-8");
		try {
			while (scanner.hasNextLine()){
				String line = scanner.nextLine();
				if(line.contains("<text>")) {
					queriesText.add(line.substring(line.indexOf("<text>")+"<text>".length(),line.indexOf("</text>")));
					queriesNames.add(line.substring(line.indexOf("<number>")+"<number>".length(),line.indexOf("</number>")));
				}
			}
		}finally{
			scanner.close();
		}
	}
	/**
	 * Transform the input string into a valid trec query
	 */
	public static String processQuery(String query){
		String transfQuery = query.replaceAll("\\W", " ").replaceAll("\\b\\s{2,}\\b", " ");
		return transfQuery;
	}
	
	/**
	 * Output results into a CSV file
	 */
	public static void writeToCsv(String fileName, String queryName, ScoredExtentResult[] results, String[] docnos, String[]titles, ParsedDocument[] docs, ArrayList<String> snippets) throws IOException{
		CSVWriter writer = new CSVWriter(new FileWriter(fileName), ',');
		String[] header = {"t_result.f_rank","t_result.f_docno","t_result.f_title","t_result.f_url","t_result.f_score","t_result.f_text","t_result.f_snippet"};
		writer.writeNext(header);
		for(int i=0; i<results.length; i++){
			String[] line = new String[7];
			line[0]=String.valueOf(i+1);
			line[1]=docnos[i];
			line[2]=titles[i];
			line[3]=getURL(docs[i].content);
			line[4]=String.valueOf(results[i].score);
			line[5]=docs[i].content;
			line[6]=snippets.get(i);
			writer.writeNext(line);
		}
		writer.close();
	}

	/**
	 * Extract the url tag from the document text and return its content
	 */
	public static String getURL(String text){
		if (text.indexOf("<url>") >= 0)
			return text.substring(text.indexOf("<url>")+"<url>".length(),text.indexOf("</url>"));
		else
			return "";
	}
}

class RetrievalProfileX {
	private String indexPath;
	private String indexName;
	private String queryPath;
	private String queryFile;
	private String rule;
	private String nrResults;
	private String resultPath;
	private String resultName;
	private String memory;
	
	public String getIndexPath() {return indexPath;}
	public String getIndexName() {return indexName;}
	public String getQueryPath() {return queryPath;}
	public String getQueryFile() {return queryFile;}
	public String getRule() {return rule;}
	public String getNrResults() {return nrResults;}
	public String getResultPath() {return resultPath;}
	public String getResultName() {return resultName;}
	public String getMemory() {return memory;}	
	
	public void setIndexName(String indexName) {this.indexName = indexName;}
	public void setResultName(String resultName) {this.resultName = resultName;}
}
