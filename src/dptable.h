#ifndef DP_TABLE_H
#define DP_TABLE_H

#include <vector>
#include <memory>

#include "columnindexingscheme.h"
#include "columniterator.h"
#include "entry.h"
#include "read.h"
#include "readset.h"

class DPTable {

 private:

  ReadSet* read_set;
  unsigned int read_count;
  bool all_heterozygous;

  // vector of indexingschemes
  std::vector<ColumnIndexingScheme*> indexers;

  // optimal score and its index in the rightmost DP table column
  unsigned int optimal_score;
  unsigned int optimal_score_index;

  // backtrace_table[x][i] indicates the index in table x from which the
  // i-th entry in the forward projection of table x comes from
  std::vector<std::vector<unsigned int>* > backtrace_table;

  // helper function to pull read ids out of read column
  std::auto_ptr<std::vector<unsigned int> > extract_read_ids(const std::vector<const Entry *>& entries);

  // helper function to compute the optimal path through the backtrace table
  std::auto_ptr<std::vector<unsigned int> > get_index_path();

  // helper function for get_unwrapped_index_path
  bool is_consistent(unsigned int index, unsigned int next_index, size_t i);

  // we need a consistent index path now that we store only half the parititions
  std::auto_ptr<std::vector<unsigned int> > get_unwrapped_index_path();

  // the function where the dp is called
  void compute_table();

 public:

  /** Constructor.  
   *
   *  @param read_set DP table is constructed for the contained
   *    reads. Ownership is retained by caller. Pointer must remain
   *    valid during the lifetime of this DPTable.
   *
   *  @param all_heterozygous If true, then the "all heterozygous"
   *    assumption is made; i.e., all positions are forced to be
   *    heterozygous even when reads suggest a homozygous site.
   *
   */
  DPTable(ReadSet* read_set, bool all_heterozygous = false);
 
  // destructor
  ~DPTable();

  unsigned int get_optimal_score();
  
  /** Computes optimal haplotypes and adds them (in the form of "super
   *  reads") to the given read_set.
   */
  void get_super_reads(ReadSet* output_read_set);

  /** Performs a backtrace through the DP table and returns optimal
   *  partitioning of the reads.  Pointer ownership is transferred to
   *  caller.
   */
  std::vector<bool>* get_optimal_partitioning();

};

#endif
