require 'test/unit'

class CircularDependencies < Exception
end

def order(job_list)
  jobs = job_list.split(',')
  all_jobs = jobs.map { |job| job.split('=>')[0] }
  dependencies = Hash[jobs.map { |job| job.split('=>') }]
  result = []
  while result.length < all_jobs.length
    all_jobs.each do |job|
      if job == dependencies[job]
        raise CircularDependencies.new
      end
      if result.include?(dependencies[job]) || dependencies[job].nil?
        if !result.include?(job)
          result << job
        end
      end
    end
  end
  result
end

class OrderedJobTest < Test::Unit::TestCase

    def test_empty_string
        assert_equal([], order(''))
    end

    def test_single_job
        assert_equal(['a'], order('a=>'))
    end

    def test_multiple_jobs
        assert_equal(['a','b','c'], order('a=>,b=>,c=>'))
    end

    def test_multiple_jobs_single_dependencies
        assert_equal(['a','c','b'],order('a=>,b=>c,c=>'))
    end

    def test_multiple_jobs_multiple_dependencies
        assert_equal(['a','d','f','c','b','e'],order('a=>,b=>c,c=>f,d=>a,e=>b,f=>'))
    end

    def test_multiple_jobs_circular_dependencies
        assert_raise(CircularDependencies) { order('a=>,b=>,c=>c') }
    end

end
