import os
from langchain.retrievers.self_query.chroma import ChromaTranslator
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import config

def get_retriever():
    embedding = OpenAIEmbeddings()
    vector_db_path = os.path.join(config.root_dir, config.chroma_directory)
    vector_db = Chroma(persist_directory=vector_db_path, embedding_function=embedding)
    
    metadata_field_info = [
    AttributeInfo(
        name="Category",
        description="""section of resume which can be 
                      `EDUCATION` - education related questions, 
                      `SKILLS` - skills experience questions, 
                      `PERSONAL DETAILS` - contact details and portfolio link, 
                      `PROFESSIONAL SUMMARY` - generic professional summary, 
                      `PUBLICATIONS` - research papers/thesis/publications, 
                      `PROFESSIONAL EXPERIENCE` - work related""", 
        type="string",
    ),
    AttributeInfo(
        name="Company Name",
        description="""Company name which can be 
                      `TDCX`, 
                      `Amdocs`, 
                      `Canon Information Technologies, Philippines Inc.`, 
                      `Willis Towers Watsons`""",
        type="string",
    ),
]
    
    document_content_description = "Resume details"
    llm = ChatOpenAI(model='gpt-4', temperature=0)
    retriever = SelfQueryRetriever.from_llm(
        llm,
        vector_db,
        document_content_description,
        metadata_field_info,
        structured_query_translator=ChromaTranslator(),
        verbose=True,
        enable_limit=False,
        search_type='similarity',
        search_kwargs={'k': 7}
    )

    return retriever
