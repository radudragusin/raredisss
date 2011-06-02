import java.io.IOException;

public class GetLinksPmcoa {
	public static void main(String[] args) throws IOException {
		
		String resourceName = "pmcoa";
		String ftpLinks = "ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/articles.*.tar.gz\n";
		
		new GetBulkLinks(resourceName,ftpLinks);

	}
}
