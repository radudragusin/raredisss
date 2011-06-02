import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import au.com.bytecode.opencsv.CSVReader;
import au.com.bytecode.opencsv.CSVWriter;

import com.google.gson.Gson;

import lemurproject.indri.ParsedDocument;
import lemurproject.indri.QueryAnnotation;
import lemurproject.indri.QueryEnvironment;
import lemurproject.indri.ScoredExtentResult;

public class RunQuery {
	
	// Setup a profile
	static RetrievalProfile profile;
	
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
		
		String paramFile;
		String defaultParamFile = "retrieval_param.json";
		String trecdocnoFile = "";
		
		if(args.length == 0 || (args.length == 1 && args[0].endsWith(".json"))){
			if(args.length == 0){
				// Use default parameter file if none is given
				paramFile = defaultParamFile;
			}else{
				// Use given parameter file
				paramFile = args[0];
			}
			
			String json = readFileAsString(paramFile);
			profile = new Gson().fromJson(json, RetrievalProfile.class);
			
			// Read the queries from file
			readQueries(profile.getQueryPath()+profile.getQueryFile());
			trecdocnoFile = profile.getIndexPath()+profile.getIndexName()+".trecdocno";
			
		}else if (args.length == 3){
			//Use the given query, the given collection, and the default param file
			paramFile = defaultParamFile;
			
			String json = readFileAsString(paramFile);
			profile = new Gson().fromJson(json, RetrievalProfile.class);
			
			String query = args[0];
			query = processQuery(query);
			
			queriesText.add(query);
			queriesNames.add(query);
			
			profile.setIndexName(args[1]);
			trecdocnoFile = profile.getIndexPath()+args[1]+".trecdocno";
			
			profile.setResultName(args[2]);
		}
		
		// Read trecdocno file -> needed in order to get the source names for the results
		List<String[]> trecRanges = readTrecdocnoFile(trecdocnoFile);
		
		// Open an Indri repository
		env.addIndex(profile.getIndexPath()+profile.getIndexName());
		
		String[] rules = new String[1];
		rules[0] = profile.getRule();
		env.setScoringRules(rules);
		env.setMemory(Long.parseLong(profile.getMemory()));
				
		// Run the queries
		for(int q=0;q<queriesText.size();q++){
			String query = queriesText.get(q);
			String queryName = queriesNames.get(q);
			
			System.out.println("Running the query: "+query);
			
			// Run an Indri query, returning the specified nr of results
			//results = env.runQuery(query, Integer.parseInt(profile.getNrResults()));
			annot = env.runAnnotatedQuery(query, Integer.parseInt(profile.getNrResults()));
			results = annot.getResults();
			
			// Fetch relevant fields of the retrieved documents 
			docnos = env.documentMetadata(results, "docno");
			titles = env.documentMetadata(results, "title");
			ParsedDocument[] docs = env.documents(results);
			
			List<String> sources = getSources(docnos,trecRanges);
			
			writeToCsv(profile.getResultPath()+profile.getResultName(),queryName,results,docnos,titles,sources,docs);
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
	public static void writeToCsv(String fileName, String queryName, ScoredExtentResult[] results, String[] docnos, String[]titles, List<String> sources, ParsedDocument[] docs) throws IOException{
		CSVWriter writer = new CSVWriter(new FileWriter(fileName), ',');
		String[] header = {"t_result.f_rank","t_result.f_docno","t_result.f_title","t_result.f_url","t_result.f_score","t_result.f_source","t_result.f_snippet","t_result.f_text"};
		writer.writeNext(header);
		for(int i=0; i<results.length; i++){
			String[] line = new String[8];
			line[0]=String.valueOf(i+1);
			line[1]=docnos[i];
			line[2]=titles[i];
			line[3]=getURL(docs[i].content);
			line[4]=String.valueOf(results[i].score);
			line[5]=sources.get(i);
			line[6]=getSnippet(docs[i].content);
			line[7]=docs[i].content;
			writer.writeNext(line);
		}
		writer.close();
	}
	/**
	 * Extract the url tag from the document text and return its content
	 */
	public static String getURL(String text){
		if (text.indexOf("<url>") >= 0)
			return "http://"+text.substring(text.indexOf("<url>")+"<url>".length(),text.indexOf("</url>"));
		else
			return "";
	}
	/**
	 * Read the trecdocno file corresponding to the index
	 * @throws IOException 
	 */
	public static List<String[]> readTrecdocnoFile(String path) throws IOException{
		CSVReader reader = new CSVReader(new FileReader(path), ',');
		List<String[]> sources = reader.readAll();
		return sources;
	}
	/**
	 * 
	 */
	public static List<String> getSources(String[] docnos, List<String[]> ranges) throws IOException{
		List<String> sources = new ArrayList<String>();
		for(String docno: docnos){
			int nr = Integer.parseInt(docno);
			for(String[] range: ranges){
				int begin = Integer.parseInt(range[2]);
				int end = Integer.parseInt(range[3]);
				if(begin <= nr && nr <= end){
					sources.add(range[0]);
				}
			}
		}
		
		// Read file containing more user frendly source text (i.e. Wikipedia for wiki)
		CSVReader reader = new CSVReader(new FileReader("sources"), ',');
		List<String[]> names = reader.readAll();
		List<String> extendedSources = new ArrayList<String>();
		for(String source: sources){
			for(String[] name: names){
				if(source.equals(name[0]))
					extendedSources.add(name[1]);
			}	
		}
		
		return extendedSources;
	}
	/**
	 * Extract first 2000 characters from the description of the document text 
	 */
	static int maxCharsInSnippet = 2000;
	public static String getSnippet(String text){
		if (text.indexOf("<description>") >= 0){
			String snippet = text.substring(text.indexOf("<description>")+"<description>".length(),text.indexOf("</description>"));
			String ellipses = "";
			if(maxCharsInSnippet < snippet.length()) ellipses = "...";
			snippet = snippet.substring(0, Math.min(maxCharsInSnippet,snippet.length()));
			if (snippet.indexOf("<!--") >= 0)
				return snippet.substring(0,snippet.indexOf("<!--"));
			return snippet+ellipses;
		}
		else if (text.indexOf("<synonyms>") >= 0) {
			String snippet = text.substring(text.indexOf("<synonyms>")+"<synonyms>".length(),text.indexOf("</synonyms>"));
			String ellipses = "";
			if(maxCharsInSnippet < snippet.length()) ellipses = "...";
			snippet = snippet.substring(0, Math.min(maxCharsInSnippet,snippet.length()));
			if (snippet.indexOf("<!--") >= 0)
				return snippet.substring(0,snippet.indexOf("<!--"));
			return snippet+ellipses;
		}
		else
			return "...";
	}
}

class RetrievalProfile {
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
