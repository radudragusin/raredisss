import java.io.IOException;


public class GetLinksWikisyn {
	public static void main(String[] args) throws IOException {
		
		String resourceName = "wikisyn";
		String link = "http://en.wikipedia.org/w/api.php?action=query&" +
				"generator=categorymembers&gcmtitle=Category:Syndromes&" +
				"gcmlimit=max&gcmdir=asc&export&exportnowrap\n";
		
		new GetBulkLinks(resourceName,link);

	}
}
