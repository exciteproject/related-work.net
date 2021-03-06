package net.relatedwork.server.neo4jHelper;

public class DBNodeProperties {
	
	// All nodes
	public static String LABEL = "label";
	public static String URI = "uri";
	public static String PAGE_RANK_VALUE = "pageRankValue";
	
	// Paper nodes
	public static String PAPER_TITLE = "title";
	public static String PAPER_ABSTRACT = "abstract";
	public static String PAPER_DATE = "date";
	public static String PAPER_ID = "source_id";
	public static String PAPER_SOURCE_URI = "source_url";
	public static String PAPER_UNMATCHED_CITATIONS = "unknown_references";
	public static String PAPER_CITATION_COUNT = "rw:citationCount";
	
	// Author nodes
	public static String AUTHOR_NAME = "name";
	
	// User nodes
	public static final String USER_EMAIL = "rw:user:foaf:email";
	public static final String USER_PW_HASH = "rw:user:pwhash";
	public static final String USER_NAME = "rw:user:foaf:name";
	public static final String USER_SESSIONS = "rw:user:sessions";
	public static final String USER_DELETED = "rw:user:deleted";
	public static final String USER_VERIFIED = "rw:user:verified";
	public static final String USER_AUTH_SECRET = "rw:user:authsecret";

    // Comment nodes
    public static final String COMMENT_URI = "rw:comment:uri";
    public static final String COMMENT_BODY = "rw:comment:body";
    public static final String COMMENT_DATE = "rw:comment:date";
    public static final String COMMENT_VOTES = "rw:comment:votes";


	// Propery values for TYPE master nodes
	public static String PAPER_LABEL_VALUE = "PAPER";
	public static String AUTHOR_LABEL_VALUE = "AUTHOR";	

	// Node index names 
	public static String SEARCH_INDEX_NAME = "fulltextSearchIdx";
	public static String URI_INDEX_NAME = "uriIdx";


}
