// JS React
// alert('Hello, from Pj & Apple!')

// testing fetches
// /api/v1/posts/, which will output valid data to the console.
// /,              which will return a 200 status code since it exists, but will fail JSON decode.
// /abadurl/,      which will return a 404 and trigger our exception.

['/api/v1/posts/', '/', '/abadurl/'].forEach(url => {
    console.log("url", url)
    fetch(url).then(response => {
        if (response.status !== 200) {
            console.log("err-200")
            throw new Error('Invalid status from server: ' + response.statusText)
        }
        console.log("ok")
        return response.json()
    }).then(data => {
        console.log("resolve")
        console.log(data)
      }).catch(e => {
        console.log("reject")
        console.error(e)
    })
})

// Post Row - TR +TD
class PostRow extends React.Component {
    render() {
        const post = this.props.post

        let thumbnail

        if (post.hero_image.thumbnail) {
            thumbnail = <img src={post.hero_image.thumbnail} />
        } else {
            thumbnail = '-'
        }

        return <tr>
            <td>{post.title}</td>
            <td>
                {thumbnail}
            </td>
            <td>{post.tags.join(', ')}</td>
            <td>{post.slug}</td>
            <td>{post.summary}</td>
            <td><a href={'/post/' + post.slug + '/'}>View</a></td>
        </tr>
    }
}

// Post Table - State, Create Rows and TR +TH
class PostTable extends React.Component {
    state = {
        dataLoaded: false,
        data: null
    }

    stateOld = {
        dataLoaded: true,
        data: {
            results: [
                {
                    id: 15,
                    tags: [
                        'django', 'react'
                    ],
                    'hero_image': {
                        'thumbnail': '/media/__sized__/hero_images/IMG_1589-4x6-thumbnail-100x100.png',
                        'full_size': '/media/hero_images/IMG_1589-4x6.png'
                    },
                    title: 'Test Post',
                    slug: 'test-post',
                    summary: 'A test post, created for Django/React.'
                }
            ]
        }
    }

    componentDidMount () {
        // fetch('/api/v1/posts/').then(response => {
        fetch(this.props.url).then(response => {
            if (response.status !== 200) {
                throw new Error('Invalid status from server: ' + response.statusText)
            }
            return response.json()
        }).then(data => {
            this.setState({dataLoaded: true, data: data })
        }).catch(e => {
        console.error(e)
        this.setState({dataLoaded: true, data: {results: []}})
        })
    }

    render() {
        let rows
        if (this.state.dataLoaded) {
            if (this.state.data.results.length) {
                rows = this.state.data.results.map(post => <PostRow post={post} key={post.id} />)
            } else {
                rows = <tr>
                    <td colSpan="6">No results found.</td>
                </tr>
            }
        } else {
            rows = <tr>
                <td colSpan="6">Loading&hellip;</td>
            </tr>
        }

        return <table className="table table-striped table-bordered mt-2">
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Image</th>
                    <th>Tags</th>
                    <th>Slug</th>
                    <th>Summary</th>
                    <th>Link</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    }
}

const domContainer = document.getElementById('react_root')
ReactDOM.render(
    React.createElement(PostTable, {url: postListUrl}),
    domContainer
)
