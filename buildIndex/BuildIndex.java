import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;

import lemurproject.indri.IndexEnvironment;
import com.google.gson.Gson;

public class BuildIndex {

	public static void main(String[] args) throws Exception {
		String paramFile = args[0];
		String json = readFileAsString(paramFile);
		IndexProfile profile = new Gson().fromJson(json, IndexProfile.class);
		
		String indexDir = profile.getIndexPath() + profile.getIndexName();
		String[] corpusFileNames = profile.getCorpusFiles();
		long memorySize = Long.parseLong(profile.getMemory()+"000000");
		
		String trecDocNos = "";
		
		// If an index of the same name exists, it will delete it
		if (deleteDir(new File(indexDir)))
			System.out.println("Deleted previous index named: " + profile.getIndexName());
		
		// Create a new index with these parameters
		IndexEnvironment env = new IndexEnvironment();
		env.setMemory(memorySize);
		env.setStemmer(profile.getStemmer());
		env.setIndexedFields(profile.getFields());
		env.create(indexDir);
		for(String filename: corpusFileNames) {
			String fname = filename + ".trec";
			env.addFile(profile.getCorpusPath()+fname,profile.getCorpusClass());
			System.out.println("Parsing file "+fname+"... docs indexed:"+env.documentsIndexed());
			trecDocNos = trecDocNos + filename + "," + readFileAsString(profile.getCorpusPath()+filename+".docno").trim().replace("\n",",") + "\n";
		}
		env.close();
		
		System.out.println("Done creating index: "+profile.getIndexName());
		
		// Copy the parameter file for future use
		writeStringToFile(json,indexDir+".param");
		System.out.println("Saved a copy of the parameter file as "+indexDir+".param");
		
		// Write the trec docno ranges for the resources
		writeStringToFile(trecDocNos,indexDir+".trecdocno");

	}
	
	private static String readFileAsString(String filePath) throws java.io.IOException{
	    byte[] buffer = new byte[(int) new File(filePath).length()];
	    FileInputStream f = new FileInputStream(filePath);
	    f.read(buffer);
	    String fileContent = new String(buffer);
	    f.close();
	    return fileContent;
	}
	
	public static boolean deleteDir(File dir) {
	    if (dir.isDirectory()) {
	        String[] children = dir.list();
	        for (int i=0; i<children.length; i++) {
	            boolean success = deleteDir(new File(dir, children[i]));
	            if (!success) {
	                return false;
	            }
	        }
	    }
	    return dir.delete();
	}
	
	public static void writeStringToFile(String content, String path) throws IOException{
		FileWriter fstream = new FileWriter(path);
		BufferedWriter out = new BufferedWriter(fstream);
		out.append(content);
		out.close();
	}
}

class IndexProfile {
	private String indexPath;
	private String indexName;
	private String corpusPath;
	private String[] corpusFiles;
	private String corpusClass;
	private String memory;
	private String stemmer;
	private String[] fields;
	
	public String getIndexPath() {return indexPath;}
	public String getIndexName() {return indexName;}
	public String getCorpusPath() {return corpusPath;}
	public String[] getCorpusFiles() {return corpusFiles;}
	public String getCorpusClass() {return corpusClass;}
	public String getMemory() {return memory;}
	public String getStemmer() {return stemmer;}
	public String[] getFields() {return fields;}
	
}